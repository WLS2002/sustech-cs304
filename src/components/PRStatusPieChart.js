import React, { useEffect, useState } from 'react';
import {
  PieChart, Pie, Tooltip, Cell, ResponsiveContainer, Legend
} from 'recharts';

const BASE_URL = '/sustech-cs304';

const STATUS_COLORS = {
  merged: '#82ca9d',   // green
  closed: '#ff8042',   // orange
  open: '#8884d8',     // purple
};

export default function PRStatusPieChart({ selectedSemester }) {
  const [data, setData] = useState([]);

  useEffect(() => {
    const DATA_URL = `${BASE_URL}/output/${selectedSemester}/pr_status_distribution.json`;

    fetch(DATA_URL)
      .then(res => res.json())
      .then(json => {
        const formattedData = Object.entries(json).map(([status, count]) => ({
          name: status,
          value: count,
        }));
        setData(formattedData);
      })
      .catch(err => {
        console.error('加载 PR 状态数据失败:', err);
        setData([]);
      });
  }, [selectedSemester]);

  return (
    <div style={{ width: '100%', height: 400 }}>
      <ResponsiveContainer width="100%" height="100%">
        <PieChart>
          <Pie
            data={data}
            dataKey="value"
            nameKey="name"
            cx="50%"
            cy="50%"
            outerRadius={130}
            label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(1)}%`}
          >
            {data.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={STATUS_COLORS[entry.name] || '#ccc'} />
            ))}
          </Pie>
          <Tooltip formatter={(value) => `${value} 个`} />
          <Legend />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
}
