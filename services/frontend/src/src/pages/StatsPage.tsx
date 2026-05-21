import { useState } from "react"
import { Header, BottomNav } from "@/components/navigation"
import { StatCard, ToggleSetting } from "@/components/stats"

export default function StatsPage() {
  const [soundEffects, setSoundEffects] = useState(true)
  const [hapticFeedback, setHapticFeedback] = useState(true)
  const [darkMode, setDarkMode] = useState(true)

  return (
    <div className="min-h-screen bg-background flex flex-col">
      <Header />
      
      <main className="flex-1 px-4 py-6 pb-24 max-w-lg mx-auto w-full">
        {/* Title */}
        <div className="mb-8">
          <h1 className="font-heading font-bold text-4xl text-primary uppercase">
            MY<br />PERFORMANCE
          </h1>
          <p className="font-sans text-muted-foreground mt-2">
            Track your Sudoku mastery over time.
          </p>
        </div>

        {/* Stat Cards */}
        <div className="space-y-4 mb-8">
          <StatCard
            label="Games Played"
            value="342"
            badge="+12 This Week"
            icon="grid_view"
            gradientFrom="#ffc300"
            gradientTo="#f97316"
            labelColor="text-accent"
            iconColor="text-accent"
          />
          
          <StatCard
            label="Average Time"
            value="14:23"
            badge="-0:45 Improvement"
            icon="timer"
            gradientFrom="#4834d4"
            gradientTo="#7c3aed"
            labelColor="text-secondary"
            iconColor="text-secondary"
          />
          
          <StatCard
            label="Best Score"
            value="98,450"
            badge="Top 5% Global"
            icon="trophy"
            gradientFrom="#dc2626"
            gradientTo="#f97316"
            labelColor="text-destructive"
            iconColor="text-destructive"
          />
        </div>

        {/* Paula Banner */}
        <div className="relative h-40 rounded-xl overflow-hidden mb-8">
          <div 
            className="absolute inset-0"
            style={{
              background: 'linear-gradient(135deg, #4834d4 0%, #f97316 50%, #ffc300 100%)'
            }}
          />
          <div className="absolute inset-0 flex items-center justify-center">
            <span 
              className="font-heading font-bold text-6xl text-white italic"
              style={{ textShadow: '3px 3px 0 #4834d4' }}
            >
              Paula
            </span>
          </div>
        </div>

        {/* Preferences */}
        <div>
          <h2 className="font-heading font-bold text-2xl text-accent uppercase mb-2">
            PREFERENCES
          </h2>
          <p className="font-sans text-muted-foreground text-sm mb-6">
            Customize your gameplay environment.
          </p>
          
          <div className="bg-card rounded-xl p-6 space-y-6 border border-border">
            <ToggleSetting
              title="Sound Effects"
              description="Blips, bloops, and victory chimes."
              checked={soundEffects}
              onChange={setSoundEffects}
            />
            
            <ToggleSetting
              title="Haptic Feedback"
              description="Feel every number placement."
              checked={hapticFeedback}
              onChange={setHapticFeedback}
            />
            
            <ToggleSetting
              title="Dark Mode"
              description="Soothe your eyes in low light."
              checked={darkMode}
              onChange={setDarkMode}
            />
          </div>
        </div>

        {/* Reset Button */}
        <button className="w-full mt-8 bg-destructive text-white font-heading font-bold text-lg py-4 rounded-xl border-2 border-destructive shadow-[4px_4px_0px_0px_var(--color-secondary)] hover:brightness-110 transition-all active:translate-y-1 active:translate-x-1 active:shadow-none">
          RESET ALL STATISTICS
        </button>
      </main>

      <BottomNav />
    </div>
  )
}
