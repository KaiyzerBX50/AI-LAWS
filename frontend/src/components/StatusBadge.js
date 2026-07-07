import React from 'react';
import { getStatusMeta } from '@/lib/lawUtils';
import { TRACKER } from '@/constants/testIds';

export const StatusBadge = ({ status, className = '' }) => {
  const meta = getStatusMeta(status);
  const Icon = meta.icon;
  return (
    <span
      data-testid={TRACKER.lawStatusBadge}
      className={`inline-flex items-center gap-1.5 rounded-full border px-2.5 py-0.5 text-xs font-medium ${meta.className} ${className}`}
    >
      <Icon className="h-3 w-3" />
      {meta.label}
    </span>
  );
};
