import React from 'react';
import { getRefinedStatusMeta } from '@/lib/lawUtils';
import { TRACKER } from '@/constants/testIds';

export const StatusBadge = ({ status, statusRaw, className = '' }) => {
  const meta = getRefinedStatusMeta(status, statusRaw);
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
