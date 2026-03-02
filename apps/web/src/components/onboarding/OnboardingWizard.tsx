"use client";
import { useState } from "react";

const STEPS = ["Welcome", "Choose Plan", "Pick Models", "Personalize", "Done"];

export function OnboardingWizard() {
  const [step, setStep] = useState(0);
  return (
    <div className="max-w-lg mx-auto p-8 space-y-6">
      <div className="flex gap-2">
        {STEPS.map((s, i) => (
          <div key={s} className={`flex-1 h-1 rounded-full transition-colors ${i <= step ? "bg-violet-600" : "bg-zinc-800"}`} />
        ))}
      </div>
      <h2 className="text-2xl font-bold text-white">{STEPS[step]}</h2>
      <div className="flex justify-between pt-4">
        <button onClick={() => setStep(s => Math.max(0, s - 1))} disabled={step === 0} className="px-4 py-2 text-zinc-400 hover:text-white disabled:opacity-30">Back</button>
        <button onClick={() => setStep(s => Math.min(STEPS.length - 1, s + 1))} className="px-5 py-2 bg-violet-600 hover:bg-violet-500 text-white rounded-xl">
          {step === STEPS.length - 1 ? "Get Started" : "Next"}
        </button>
      </div>
    </div>
  );
}
