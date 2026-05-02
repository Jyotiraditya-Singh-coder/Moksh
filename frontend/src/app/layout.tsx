import type { Metadata } from 'next';
import { ClerkProvider } from '@clerk/nextjs';
import 'bootstrap/dist/css/bootstrap.min.css';
import '@/styles/tailwind.css';
import '@/styles/index.css';
import Header from '@/components/ui/Header';
import Footer from '@/components/ui/Footer';
import ClientLayout from './ClientLayout';
import UserSync from '@/components/UserSync';

export const metadata: Metadata = {
  title: 'EduNex AI - Personalized AI Education Intelligence',
  description:
    'Experience the future of learning with AI-powered education tools, adaptive challenges, predictive analytics, and multilingual voice tutoring.',
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <ClerkProvider>
      <html lang="en">
        <body>
          <ClientLayout>
            <UserSync />
            <Header />
            <main>{children}</main>
            <Footer />
          </ClientLayout>
        </body>
      </html>
    </ClerkProvider>
  );
}
