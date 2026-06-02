// import React from 'react';
// import type { Metadata, Viewport } from 'next';
// import '../styles/index.css';

// export const viewport: Viewport = {
//   width: 'device-width',
//   initialScale: 1,
// };

// export const metadata: Metadata = {
//   title: 'Next.js with Tailwind CSS',
//   description: 'A boilerplate project with Next.js and Tailwind CSS',
//   icons: {
//     icon: [
//       { url: '/assets/images/app_logo1.png', type: 'image/x-icon' }
//     ],
//   },
// };

// export default function RootLayout({
//   children,
// }: Readonly<{
//   children: React.ReactNode;
// }>) {
//   return (
//     <html lang="en">
//       <body>{children}

//         <script type="module" async src="https://static.rocket.new/rocket-web.js?_cfg=https%3A%2F%2Fneurospace9758back.builtwithrocket.new&_be=https%3A%2F%2Fappanalytics.rocket.new&_v=0.1.17" />
//         <script type="module" defer src="https://static.rocket.new/rocket-shot.js?v=0.0.2" /></body>
//     </html>
//   );
// }

import React from 'react';
import type { Metadata, Viewport } from 'next';
import '../styles/index.css';
import { Toaster } from 'sonner'; // <-- import Toaster

export const viewport: Viewport = {
  width: 'device-width',
  initialScale: 1,
};

export const metadata: Metadata = {
  title: 'Next.js with Tailwind CSS',
  description: 'A boilerplate project with Next.js and Tailwind CSS',
  icons: {
    icon: [
      { url: '/assets/images/app_logo1.png', type: 'image/x-icon' }
    ],
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>
        {children}

        {/* Toaster global pour les notifications */}
        <Toaster position="top-right" richColors />

        <script
          type="module"
          async
          src="https://static.rocket.new/rocket-web.js?_cfg=https%3A%2F%2Fneurospace9758back.builtwithrocket.new&_be=https%3A%2F%2Fappanalytics.rocket.new&_v=0.1.17"
        />
        <script
          type="module"
          defer
          src="https://static.rocket.new/rocket-shot.js?v=0.0.2"
        />
      </body>
    </html>
  );
}