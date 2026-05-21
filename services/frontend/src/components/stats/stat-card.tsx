import { cn } from "@/lib/utils"

interface StatCardProps {
  label: string
  value: string
  badge?: string
  icon: string
  gradientFrom: string
  gradientTo: string
  labelColor?: string
  iconColor?: string
  badgeColor?: string
  badgeBgColor?: string
}

export function StatCard({
  label,
  value,
  badge,
  icon,
  gradientFrom,
  gradientTo,
  labelColor = "text-accent",
  iconColor = "text-accent",
  badgeColor = "text-primary",
  badgeBgColor = "bg-primary/10",
}: StatCardProps) {
  return (
    <div className="bg-secondary border-2 border-accent rounded-lg relative overflow-hidden shadow-[4px_4px_0px_0px_var(--color-accent)]">
      <div 
        className="h-12 opacity-80"
        style={{ 
          background: `linear-gradient(to right, ${gradientFrom}, ${gradientTo})`,
          maskImage: 'url("data:image/svg+xml,%3Csvg viewBox=\'0 0 100 20\' xmlns=\'http://www.w3.org/2000/svg\'%3E%3Cpath d=\'M0 0 L100 0 L100 15 Q75 20 50 15 Q25 10 0 15 Z\' fill=\'black\'/%3E%3C/svg%3E")',
          WebkitMaskImage: 'url("data:image/svg+xml,%3Csvg viewBox=\'0 0 100 20\' xmlns=\'http://www.w3.org/2000/svg\'%3E%3Cpath d=\'M0 0 L100 0 L100 15 Q75 20 50 15 Q25 10 0 15 Z\' fill=\'black\'/%3E%3C/svg%3E")',
          maskSize: '100% 100%',
          WebkitMaskSize: '100% 100%'
        }}
      />
      <div className="p-6">
        <div className="flex items-center justify-between mb-4">
          <span className={cn("font-mono text-xs uppercase tracking-widest", labelColor)}>
            {label}
          </span>
          <span 
            className={cn("material-symbols-outlined", iconColor)}
            style={{ fontVariationSettings: "'FILL' 1" }}
          >
            {icon}
          </span>
        </div>
        <div className="font-sans text-4xl font-extrabold text-foreground">{value}</div>
        {badge && (
          <div className={cn("mt-4 font-mono text-xs rounded px-2 py-1 uppercase inline-block", badgeColor, badgeBgColor)}>
            {badge}
          </div>
        )}
      </div>
    </div>
  )
}

interface ToggleSettingProps {
  title: string
  description: string
  checked?: boolean
  onChange?: (checked: boolean) => void
}

export function ToggleSetting({ title, description, checked = false, onChange }: ToggleSettingProps) {
  return (
    <div className="flex items-center justify-between">
      <div>
        <div className="font-sans font-bold text-foreground">{title}</div>
        <div className="font-mono text-xs text-muted-foreground mt-1">{description}</div>
      </div>
      <label className="relative inline-flex items-center cursor-pointer">
        <input 
          type="checkbox" 
          className="sr-only peer" 
          checked={checked}
          onChange={(e) => onChange?.(e.target.checked)}
        />
        <div className="w-14 h-7 bg-muted peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-6 after:w-6 after:transition-all peer-checked:bg-accent" />
      </label>
    </div>
  )
}
