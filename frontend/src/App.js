import UploadForm from "./components/UploadForm";
import History from "./components/History";

export default function App() {
  return (
    <div className="bg-green-50 min-h-screen">
      <header className="bg-gradient-to-r from-green-700 to-green-500 p-6 text-center text-white shadow-lg">
        <h1 className="text-4xl font-bold flex items-center justify-center gap-2">
          🌿 Airy Ai Project
        </h1>
        <p className="text-lg mt-2">
          Advanced Deep Learning Plant Disease Detection System
        </p>
        <p className="text-sm opacity-90">
          AI-powered diagnosis with 85%+ accuracy • CNN-based image analysis
        </p>
      </header>

      <section className="max-w-7xl mx-auto p-8 flex flex-col lg:flex-row gap-10">
        {/* Upload Card */}
        <UploadForm />

        {/* Recent Scans Section (Static Example) */}
        <div className="bg-white w-full lg:w-2/5 p-6 rounded-xl shadow-md">
          <h3 className="font-semibold text-lg mb-4 flex items-center gap-2">
            🔄 Recent Scans (10)
          </h3>

          <div className="h-[400px] overflow-y-scroll pr-2 space-y-4">
            <div className="flex gap-4 bg-gray-50 p-3 rounded-lg shadow-sm">
              <img src="https://via.placeholder.com/80" className="w-20 h-20 rounded-md" />
              <div>
                <h4 className="font-semibold">Bacterial Leaf Spot</h4>
                <p className="text-sm text-gray-600">
                  Unknown (possibly a type of vegetable or fruit leaf)
                </p>
                <span className="text-orange-600 text-xs font-medium bg-orange-100 px-2 py-1 rounded">
                  Moderate
                </span>
                <span className="text-gray-500 text-xs ml-2">75% • Nov 4, 2025</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      <footer className="bg-gray-900 text-center text-gray-300 p-6 mt-10">
        <h2 className="font-semibold text-white text-lg">🌿 Airy Ai Project</h2>
        <p className="text-sm mt-1">
          Empowering farmers with AI-driven plant health diagnostics
        </p>
        <p className="text-sm mt-2">
          Developed by <span className="text-green-400 font-medium">Harsh Vardhan Singh</span>
        </p>
      </footer>
    </div>
  );
}
