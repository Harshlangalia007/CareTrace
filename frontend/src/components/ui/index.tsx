import React from 'react';

interface BadgeProps {
  variant?: 'default' | 'success' | 'warning' | 'danger' | 'purple' | 'accent';
  children: React.ReactNode;
  size?: 'sm' | 'md';
}

const variantStyles: Record<string, React.CSSProperties> = {
  default: { background: 'var(--surface-2)', color: 'var(--text-muted)' },
  success: { background: 'var(--success-bg)', color: 'var(--success)' },
  warning: { background: 'var(--warning-bg)', color: 'var(--warning)' },
  danger: { background: 'var(--danger-bg)', color: 'var(--danger)' },
  purple: { background: 'var(--purple-bg)', color: 'var(--purple)' },
  accent: { background: 'var(--accent-bg)', color: 'var(--accent)' },
};

export const Badge: React.FC<BadgeProps> = ({ variant = 'default', children, size = 'sm' }) => (
  <span style={{
    ...variantStyles[variant],
    padding: size === 'sm' ? '2px 8px' : '4px 10px',
    borderRadius: 99,
    fontSize: 11,
    fontWeight: 600,
    letterSpacing: '0.02em',
    textTransform: 'uppercase',
    display: 'inline-block',
    whiteSpace: 'nowrap',
  }}>
    {children}
  </span>
);

interface CardProps {
  children: React.ReactNode;
  style?: React.CSSProperties;
  className?: string;
  onClick?: () => void;
}

export const Card: React.FC<CardProps> = ({ children, style, className, onClick }) => (
  <div
    className={className}
    onClick={onClick}
    style={{
      background: 'var(--bg)',
      border: '1px solid var(--border)',
      borderRadius: 'var(--radius-lg)',
      padding: '20px',
      boxShadow: 'var(--shadow)',
      cursor: onClick ? 'pointer' : undefined,
      ...style,
    }}
  >
    {children}
  </div>
);

interface SectionHeaderProps {
  title: string;
  subtitle?: string;
  count?: number;
  actions?: React.ReactNode;
}

export const SectionHeader: React.FC<SectionHeaderProps> = ({ title, subtitle, count, actions }) => (
  <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 16 }}>
    <div>
      <h3 style={{ fontSize: 14, fontWeight: 700, letterSpacing: '0.04em', textTransform: 'uppercase', color: 'var(--text-muted)', display: 'flex', alignItems: 'center', gap: 8 }}>
        {title}
        {count !== undefined && (
          <span style={{ background: 'var(--surface-2)', color: 'var(--text-muted)', borderRadius: 99, padding: '1px 7px', fontSize: 11, fontWeight: 700 }}>
            {count}
          </span>
        )}
      </h3>
      {subtitle && <p style={{ fontSize: 12, color: 'var(--text-subtle)', marginTop: 2 }}>{subtitle}</p>}
    </div>
    {actions && <div>{actions}</div>}
  </div>
);

interface StatusDotProps {
  status: 'green' | 'yellow' | 'red' | 'blue' | 'gray';
}

const dotColors = {
  green: 'var(--success)',
  yellow: 'var(--warning)',
  red: 'var(--danger)',
  blue: 'var(--accent)',
  gray: 'var(--text-subtle)',
};

export const StatusDot: React.FC<StatusDotProps> = ({ status }) => (
  <span style={{
    display: 'inline-block',
    width: 8,
    height: 8,
    borderRadius: '50%',
    background: dotColors[status],
    flexShrink: 0,
  }} />
);

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'ghost' | 'danger';
  size?: 'sm' | 'md' | 'lg';
  loading?: boolean;
}

export const Button: React.FC<ButtonProps> = ({
  variant = 'primary', size = 'md', loading, children, style, disabled, ...props
}) => {
  const base: React.CSSProperties = {
    display: 'inline-flex', alignItems: 'center', justifyContent: 'center',
    gap: 6, fontWeight: 600, borderRadius: 'var(--radius)',
    border: '1px solid transparent', transition: 'all 0.15s',
    cursor: disabled || loading ? 'not-allowed' : 'pointer',
    opacity: disabled || loading ? 0.6 : 1,
    whiteSpace: 'nowrap',
    fontSize: size === 'sm' ? 12 : size === 'lg' ? 15 : 13,
    padding: size === 'sm' ? '5px 12px' : size === 'lg' ? '10px 20px' : '7px 14px',
  };
  const variants: Record<string, React.CSSProperties> = {
    primary: { background: 'var(--text)', color: 'var(--bg)', borderColor: 'var(--text)' },
    secondary: { background: 'var(--surface)', color: 'var(--text)', borderColor: 'var(--border)' },
    ghost: { background: 'transparent', color: 'var(--text-muted)', borderColor: 'transparent' },
    danger: { background: 'var(--danger-bg)', color: 'var(--danger)', borderColor: 'var(--danger)' },
  };

  return (
    <button style={{ ...base, ...variants[variant], ...style }} disabled={disabled || loading} {...props}>
      {loading ? 'Loading…' : children}
    </button>
  );
};

export const Divider: React.FC<{ style?: React.CSSProperties }> = ({ style }) => (
  <hr style={{ border: 'none', borderTop: '1px solid var(--border)', margin: '16px 0', ...style }} />
);

interface SourceBadgeProps {
  title?: string;
  date?: string;
  onClick?: () => void;
}

export const SourceBadge: React.FC<SourceBadgeProps> = ({ title, date, onClick }) => (
  <button
    onClick={onClick}
    style={{
      display: 'inline-flex', alignItems: 'center', gap: 5,
      background: 'var(--accent-bg)', color: 'var(--accent)',
      border: '1px solid var(--accent)', borderRadius: 'var(--radius)',
      padding: '3px 10px', fontSize: 11, fontWeight: 600,
      cursor: onClick ? 'pointer' : 'default',
      letterSpacing: '0.02em',
    }}
  >
    <span>SOURCE</span>
    {title && <span style={{ fontWeight: 400 }}>{title}</span>}
    {date && <span style={{ fontWeight: 400, color: 'var(--text-muted)' }}>— {date}</span>}
  </button>
);

export const EmptyState: React.FC<{ icon?: string; title: string; subtitle?: string }> = ({
  icon, title, subtitle
}) => (
  <div style={{ textAlign: 'center', padding: '48px 24px', color: 'var(--text-subtle)' }}>
    {icon && <div style={{ fontSize: 32, marginBottom: 12 }}>{icon}</div>}
    <div style={{ fontWeight: 600, fontSize: 15, color: 'var(--text-muted)', marginBottom: 4 }}>{title}</div>
    {subtitle && <div style={{ fontSize: 13 }}>{subtitle}</div>}
  </div>
);

export const Spinner: React.FC = () => (
  <div style={{ display: 'inline-block', width: 18, height: 18, border: '2px solid var(--border)', borderTopColor: 'var(--accent)', borderRadius: '50%', animation: 'spin 0.7s linear infinite' }}>
    <style>{`@keyframes spin { to { transform: rotate(360deg); } }`}</style>
  </div>
);
