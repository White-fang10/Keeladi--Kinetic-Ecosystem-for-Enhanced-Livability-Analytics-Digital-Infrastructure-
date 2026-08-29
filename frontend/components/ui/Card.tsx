'use client';

import React from 'react';
import styles from './Card.module.css';

interface CardProps {
  children: React.ReactNode;
  className?: string;
  padding?: 'none' | 'sm' | 'md' | 'lg';
  hover?: boolean;
  glass?: boolean;
  onClick?: () => void;
}

export default function Card({
  children,
  className = '',
  padding = 'lg',
  hover = true,
  glass = false,
  onClick,
}: CardProps) {
  return (
    <div
      className={[
        styles.card,
        styles[`pad-${padding}`],
        hover ? styles.hover : '',
        glass ? styles.glass : '',
        className,
      ].join(' ')}
      onClick={onClick}
      style={onClick ? { cursor: 'pointer' } : undefined}
    >
      {children}
    </div>
  );
}
