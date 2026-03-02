export function WelcomeScreen() {
  return (
    <div className="text-center space-y-4">
      <div className="w-16 h-16 rounded-2xl bg-violet-600 mx-auto flex items-center justify-center">
        <span className="text-white font-bold text-2xl">C</span>
      </div>
      <h1 className="text-3xl font-bold text-white">Welcome to Cleus</h1>
      <p className="text-zinc-400 max-w-sm mx-auto">The world's first uncensored multimodal AI platform. Let's get you set up.</p>
    </div>
  );
}
