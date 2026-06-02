import fs from 'fs/promises';
import nodemailer from 'nodemailer';

type SendTrainingReportEmailParams = {
  toEmail: string;
  toName?: string;
  fileId: string;
  pdfPath: string;
  jsonPath?: string;
  modelName?: string;
  accuracy?: string | number;
  createdAt?: string;
};

async function fileExists(filePath?: string) {
  if (!filePath) return false;
  try {
    await fs.access(filePath);
    return true;
  } catch {
    return false;
  }
}

export async function sendTrainingReportEmail({
  toEmail,
  toName = 'User',
  fileId,
  pdfPath,
  jsonPath,
  modelName = 'Training Model',
  accuracy = 'N/A',
  createdAt = new Date().toISOString(),
}: SendTrainingReportEmailParams) {
  try {
    if (!(await fileExists(pdfPath))) {
      return { success: false, error: 'PDF report not found' };
    }

    if (!process.env.BREVO_SMTP_USER || !process.env.BREVO_SMTP_PASSWORD) {
      return { success: false, error: 'Brevo SMTP credentials are not configured' };
    }

    const transporter = nodemailer.createTransport({
      host: process.env.BREVO_SMTP_HOST || 'smtp-relay.brevo.com',
      port: Number(process.env.BREVO_SMTP_PORT || 587),
      secure: false,
      auth: {
        user: process.env.BREVO_SMTP_USER,
        pass: process.env.BREVO_SMTP_PASSWORD,
      },
    });

    const attachments = [
      {
        filename: 'report.pdf',
        path: pdfPath,
      },
    ];

    if (await fileExists(jsonPath)) {
      attachments.push({
        filename: 'results.json',
        path: jsonPath!,
      });
    }

    const info = await transporter.sendMail({
      from: process.env.EMAIL_FROM || 'NeuroSpace <onboarding@resend.dev>',
      to: toEmail,
      subject: 'Your NeuroSpace Training Report is Ready',
      text: `Hello ${toName},

Your model training and classification process has been completed successfully.

The generated PDF report is attached to this email. It contains your classification results, performance metrics, and training summary.

Job ID: ${fileId}
Model: ${modelName}
Accuracy: ${accuracy}
Generated at: ${createdAt}

Thank you for using NeuroSpace.

Best regards,
NeuroSpace Team`,
      attachments,
    });

    return { success: true, data: info };
  } catch (error) {
    return {
      success: false,
      error: error instanceof Error ? error.message : 'Failed to send training report email',
    };
  }
}
