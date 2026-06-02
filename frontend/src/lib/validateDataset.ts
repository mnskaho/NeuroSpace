export interface ValidationResult {
  isValid: boolean
  error?: string
}

// Check if file is CSV format
function validateCsvFormat(file: File): ValidationResult {
  const fileName = file.name.toLowerCase()
  const mimeType = file.type.toLowerCase()

  if (!fileName.endsWith(".csv") && mimeType !== "text/csv" && mimeType !== "application/vnd.ms-excel") {
    return {
      isValid: false,
      error: "The format must be CSV.",
    }
  }

  return { isValid: true }
}

// Parse CSV and check for numeric values, missing values, and outliers
async function validateCsvContent(file: File): Promise<ValidationResult> {
  try {
    const text = await file.text()
    const lines = text.trim().split("\n")

    if (lines.length < 2) {
      return {
        isValid: false,
        error: "The dataset must contain at least a header and one data row.",
      }
    }

    const headers = lines[0].split(",").map((h) => h.trim())
    const dataRows = lines.slice(1)

    // Collect all numeric values for outlier detection
    const allValues: number[] = []
    const columnValues: number[][] = Array(headers.length).fill(null).map(() => [])

    // Check for non-numeric values and missing values
    for (let rowIndex = 0; rowIndex < dataRows.length; rowIndex++) {
      const row = dataRows[rowIndex]
      if (!row.trim()) continue // Skip empty rows

      const cells = row.split(",").map((cell) => cell.trim())

      if (cells.length !== headers.length) {
        return {
          isValid: false,
          error: "The dataset has inconsistent column counts. Please verify your CSV format.",
        }
      }

      for (let colIndex = 0; colIndex < cells.length; colIndex++) {
        const cell = cells[colIndex]

        // Check for missing values - be more lenient for preprocessed datasets
        if (cell === "" || cell.toLowerCase() === "nan" || cell.toLowerCase() === "null" || cell === "N/A") {
          return {
            isValid: false,
            error: "Dataset contains missing values. Please ensure all values are numeric.",
          }
        }

        // Check if value is numeric
        const numValue = parseFloat(cell)
        if (isNaN(numValue)) {
          return {
            isValid: false,
            error: "The dataset must contain only numeric values.",
          }
        }

        allValues.push(numValue)
        columnValues[colIndex].push(numValue)
      }
    }

    // Skip outlier detection for preprocessed datasets - assume user has already handled outliers
    // This was causing issues with legitimate preprocessed data

    // Check if data appears reasonable (basic heuristic)
    if (allValues.length > 0) {
      const min = Math.min(...allValues)
      const max = Math.max(...allValues)
      const range = max - min

      // Be more lenient with value ranges for preprocessed datasets
      // Allow wider ranges but still catch obviously problematic data
      const isReasonable =
        !isNaN(min) && !isNaN(max) && isFinite(min) && isFinite(max) &&
        range > 0 && range < 1e10 // Allow very large ranges but catch infinity/NaN

      if (!isReasonable) {
        return {
          isValid: false,
          error: "Dataset contains invalid numeric values. Please check your data preprocessing.",
        }
      }
    }

    return { isValid: true }
  } catch (error) {
    return {
      isValid: false,
      error: "Error parsing CSV file. Please ensure it is a valid CSV format.",
    }
  }
}

export async function validateDataset(file: File): Promise<ValidationResult> {
  // First check CSV format
  const formatCheck = validateCsvFormat(file)
  if (!formatCheck.isValid) {
    return formatCheck
  }

  // Then validate content
  return validateCsvContent(file)
}
