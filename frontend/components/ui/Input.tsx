'use client';

import React, { forwardRef } from 'react';
import styles from './Input.module.css';

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  leftIcon?: React.ReactNode;
}

const Input = forwardRef<HTMLInputElement, InputProps>(
  ({ label, error, leftIcon, className = '', ...props }, ref) => {
    return (
      <div className={[styles.wrapper, className].join(' ')}>
        {label && <label className={styles.label}>{label}</label>}
        <div className={styles.inputContainer}>
          {leftIcon && <span className={styles.icon}>{leftIcon}</span>}
          <input
            ref={ref}
            className={[
              styles.input,
              leftIcon ? styles.hasLeftIcon : '',
              error ? styles.hasError : '',
            ].join(' ')}
            {...props}
          />
        </div>
        {error && <span className={styles.errorText}>{error}</span>}
      </div>
    );
  }
);

Input.displayName = 'Input';
export default Input;
