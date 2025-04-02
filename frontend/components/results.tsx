"use client";
import React from 'react';
import { Card } from '@radix-ui/themes';

const renderNestedCards = (data: Record<string, any>) => {
  if (typeof data !== 'object' || data === null) {
    return <span>{String(data)}</span>;
  }
  return (
    <div className="grid grid-cols-1 gap-4">
      {Object.entries(data).map(([key, value]) => (
        <Card key={key} className="p-4">
          <div className="font-semibold text-gray-700">{key}</div>
          <div className="mt-2 text-gray-600">
            {typeof value === 'object'
              ? renderNestedCards(value)
              : String(value)}
          </div>
        </Card>
      ))}
    </div>
  );
};

export const DisplayResults = ({ jsonData }: { jsonData: Record<string, any> }) => {
  return (
    <div className="grid grid-cols-1 gap-4 w-full">
      {Object.entries(jsonData).map(([key, value]) => (
        <Card key={key} className="p-4">
          <div className="font-semibold text-gray-700">{key}</div>
          <div className="mt-2 text-gray-600">
            {typeof value === 'object'
              ? renderNestedCards(value)
              : String(value)}
          </div>
        </Card>
      ))}
    </div>
  );
};