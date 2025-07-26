'use client';

import { useEffect, useState } from 'react';

export default function Dashboard() {
  const [studentName, setStudentName] = useState('طالب');

  useEffect(() => {
    const storedEmail = localStorage.getItem('student_email') || '';
    if (storedEmail) {
      const namePart = storedEmail.split('@')[0];
      const fullName = namePart
        .replace(/[._\d]/g, ' ')
        .replace(/\s+/g, ' ')
        .trim();
      setStudentName(fullName);
    }
  }, []);

  return (
    <div
      className="min-h-screen bg-cover bg-center text-white"
      style={{ backgroundImage: "url('/university-bg.jpg')" }}
    >
      <header className="flex items-center justify-between px-8 py-5 bg-blue-900 bg-opacity-90 shadow">
        <div className="flex items-center space-x-4">
          <img src="/faculty-logo.png" alt="Faculty Logo" className="w-10 h-10 rounded-full" />
          <h1 className="text-xl font-bold text-white">كلية الحاسبات والمعلومات - جامعة أسيوط</h1>
          <img src="/assiut-logo.png" alt="University Logo" className="w-10 h-10 rounded-full" />
        </div>
        <nav className="flex space-x-4">
          <a href="/login" className="text-white hover:underline font-semibold">تسجيل الدخول</a>
          <a href="/complaints" className="text-white hover:underline font-semibold">الشكاوى</a>
          <a href="/suggestions" className="text-white hover:underline font-semibold">الاقتراحات</a>
          <a href="/chat" className="text-white hover:underline font-semibold">بوت الدردشة</a>
        </nav>
      </header>

      <section className="flex items-center justify-center h-[70vh] px-4">
        <div className="text-center bg-white bg-opacity-80 p-8 rounded-lg shadow max-w-3xl">
          <h2 className="text-4xl md:text-5xl font-bold text-blue-900 mb-4">
            👋 مرحبًا بك يا {studentName}
          </h2>
          <h3 className="text-2xl font-semibold text-gray-700 mb-2">
            Welcome to the Student Dashboard
          </h3>
          <p className="text-gray-600 text-lg mt-2">
            استخدم شريط التنقل أعلاه للوصول إلى أي قسم بمنتهى السهولة.
          </p>
        </div>
      </section>
    </div>
  );
}
