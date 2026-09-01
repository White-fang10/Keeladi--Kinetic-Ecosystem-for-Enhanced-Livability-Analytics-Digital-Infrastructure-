/**
 * KEELADI Logo SVG Placeholder
 * Replace with actual logo.svg when available.
 * Maintains the inverted-pyramid brand concept.
 */

interface LogoProps {
  size?: number;
  variant?: 'full' | 'icon';
  className?: string;
}

export default function Logo({ size = 36, variant = 'full', className = '' }: LogoProps) {
  return (
    <div className={`logo-wrapper ${className}`} style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
      {/* SVG Placeholder — replace inner content with actual logo.svg */}
      <svg
        width={size}
        height={size}
        viewBox="0 0 36 36"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
        aria-label="KEELADI Logo"
      >
        {/* Inverted pyramid — symbolises Intelligence Funnel → Citizen Impact */}
        <rect width="36" height="36" rx="10" fill="#E6FF2B" />
        <polygon
          points="6,8 30,8 24,18 12,18"
          fill="#0B4550"
          opacity="0.9"
        />
        <polygon
          points="12,20 24,20 21,27 15,27"
          fill="#0B4550"
          opacity="0.7"
        />
        <polygon
          points="15,29 21,29 18,34 18,34"
          fill="#0B4550"
          opacity="0.5"
        />
      </svg>

      {variant === 'full' && (
        <div style={{ lineHeight: 1 }}>
          <div style={{
            fontFamily: 'var(--font-sans)',
            fontWeight: 700,
            fontSize: size * 0.5,
            color: 'var(--accent)',
            letterSpacing: '0.08em',
          }}>
            KEELADI
          </div>
          <div style={{
            fontFamily: 'var(--font-sans)',
            fontWeight: 400,
            fontSize: size * 0.25,
            color: 'var(--text-secondary)',
            letterSpacing: '0.04em',
          }}>
            Smart Civic Platform
          </div>
        </div>
      )}
    </div>
  );
}
