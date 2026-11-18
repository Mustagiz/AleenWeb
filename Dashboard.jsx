import React from 'react';
import {
  Home, Chart, Chart2, Wallet, Money, Users, User,
  Setting, Notification, Search, Filter, Calendar,
  TrendUp, TrendDown, More, Add, Edit, Trash,
  Bell, Mail, Eye, Lock, Logout, Grid, List,
} from 'iconsax-react';

const stats = [
  { label: 'Revenue', value: '$48,290', delta: '+12.4%', up: true, icon: Money },
  { label: 'Users', value: '12,847', delta: '+3.1%', up: true, icon: Users },
  { label: 'Orders', value: '1,204', delta: '-1.8%', up: false, icon: Chart },
  { label: 'Conversion', value: '3.42%', delta: '+0.6%', up: true, icon: TrendUp },
];

const rows = [
  { id: 1, name: 'Acme Corp', email: 'ops@acme.com', status: 'Active', amount: '$4,200' },
  { id: 2, name: 'Globex', email: 'billing@globex.io', status: 'Pending', amount: '$1,800' },
  { id: 3, name: 'Initech', email: 'finance@initech.com', status: 'Active', amount: '$6,500' },
  { id: 4, name: 'Umbrella', email: 'ap@umbrella.co', status: 'Overdue', amount: '$920' },
];

const iconProps = { size: 20, color: '#64748b', variant: 'Linear' };

export default function Dashboard() {
  return (
    <div style={{ display: 'flex', minHeight: '100vh', background: '#f8fafc', fontFamily: 'system-ui, sans-serif' }}>
      {/* Sidebar */}
      <aside style={{ width: 240, background: '#0f172a', color: '#e2e8f0', padding: '24px 16px', display: 'flex', flexDirection: 'column', gap: 8 }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 24, paddingLeft: 8 }}>
          <Grid size={24} color="#38bdf8" variant="Linear" />
          <span style={{ fontWeight: 700, fontSize: 18 }}>Acme Dashboard</span>
        </div>
        {[
          { label: 'Overview', icon: Home },
          { label: 'Analytics', icon: Chart2 },
          { label: 'Customers', icon: Users },
          { label: 'Billing', icon: Wallet },
          { label: 'Settings', icon: Setting },
        ].map(({ label, icon: Icon }) => (
          <button key={label} style={{ display: 'flex', alignItems: 'center', gap: 12, padding: '10px 12px', background: label === 'Overview' ? '#1e293b' : 'transparent', border: 'none', color: '#e2e8f0', borderRadius: 8, cursor: 'pointer', textAlign: 'left', width: '100%' }}>
            <Icon {...iconProps} color={label === 'Overview' ? '#38bdf8' : '#94a3b8'} />
            <span style={{ fontSize: 14 }}>{label}</span>
          </button>
        ))}
        <div style={{ marginTop: 'auto', padding: '12px 8px', borderTop: '1px solid #1e293b', display: 'flex', alignItems: 'center', gap: 10 }}>
          <User size={20} color="#94a3b8" variant="Linear" />
          <span style={{ fontSize: 13 }}>Mustagiz J.</span>
          <Logout size={18} color="#94a3b8" variant="Linear" style={{ marginLeft: 'auto', cursor: 'pointer' }} />
        </div>
      </aside>

      {/* Main */}
      <main style={{ flex: 1, padding: 24, display: 'flex', flexDirection: 'column', gap: 24 }}>
        {/* Top bar */}
        <header style={{ display: 'flex', alignItems: 'center', gap: 16 }}>
          <div style={{ flex: 1, position: 'relative' }}>
            <Search size={18} color="#94a3b8" variant="Linear" style={{ position: 'absolute', left: 12, top: 10 }} />
            <input placeholder="Search..." style={{ width: '100%', padding: '10px 12px 10px 40px', border: '1px solid #e2e8f0', borderRadius: 8, fontSize: 14, background: '#fff' }} />
          </div>
          <button style={{ background: '#fff', border: '1px solid #e2e8f0', borderRadius: 8, padding: 10, cursor: 'pointer' }}>
            <Filter size={18} color="#64748b" variant="Linear" />
          </button>
          <button style={{ background: '#fff', border: '1px solid #e2e8f0', borderRadius: 8, padding: 10, cursor: 'pointer', position: 'relative' }}>
            <Bell size={18} color="#64748b" variant="Linear" />
            <span style={{ position: 'absolute', top: 6, right: 6, width: 8, height: 8, background: '#ef4444', borderRadius: '50%' }} />
          </button>
          <button style={{ background: '#2563eb', color: '#fff', border: 'none', borderRadius: 8, padding: '10px 16px', display: 'flex', alignItems: 'center', gap: 8, cursor: 'pointer', fontSize: 14, fontWeight: 600 }}>
            <Add size={18} color="#fff" variant="Linear" /> New
          </button>
        </header>

        {/* Stats */}
        <section style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 16 }}>
          {stats.map(({ label, value, delta, up, icon: Icon }) => (
            <div key={label} style={{ background: '#fff', borderRadius: 12, padding: 20, border: '1px solid #e2e8f0' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 12 }}>
                <span style={{ fontSize: 13, color: '#64748b' }}>{label}</span>
                <Icon size={20} color="#94a3b8" variant="Linear" />
              </div>
              <div style={{ fontSize: 24, fontWeight: 700, marginBottom: 4 }}>{value}</div>
              <div style={{ display: 'flex', alignItems: 'center', gap: 4, fontSize: 13, color: up ? '#16a34a' : '#dc2626' }}>
                {up ? <TrendUp size={14} color="#16a34a" variant="Linear" /> : <TrendDown size={14} color="#dc2626" variant="Linear" />}
                {delta}
              </div>
            </div>
          ))}
        </section>

        {/* Table */}
        <section style={{ background: '#fff', borderRadius: 12, border: '1px solid #e2e8f0', overflow: 'hidden' }}>
          <div style={{ padding: '16px 20px', borderBottom: '1px solid #e2e8f0', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <h3 style={{ margin: 0, fontSize: 16, fontWeight: 600 }}>Recent Customers</h3>
            <div style={{ display: 'flex', gap: 8 }}>
              <button style={{ background: '#f1f5f9', border: 'none', borderRadius: 6, padding: 8, cursor: 'pointer' }}><Calendar size={16} color="#64748b" variant="Linear" /></button>
              <button style={{ background: '#f1f5f9', border: 'none', borderRadius: 6, padding: 8, cursor: 'pointer' }}><More size={16} color="#64748b" variant="Linear" /></button>
            </div>
          </div>
          <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: 14 }}>
            <thead>
              <tr style={{ background: '#f8fafc', textAlign: 'left' }}>
                <th style={{ padding: '12px 20px', color: '#64748b', fontWeight: 500 }}>Name</th>
                <th style={{ padding: '12px 20px', color: '#64748b', fontWeight: 500 }}>Email</th>
                <th style={{ padding: '12px 20px', color: '#64748b', fontWeight: 500 }}>Status</th>
                <th style={{ padding: '12px 20px', color: '#64748b', fontWeight: 500 }}>Amount</th>
                <th style={{ padding: '12px 20px', color: '#64748b', fontWeight: 500 }}></th>
              </tr>
            </thead>
            <tbody>
              {rows.map((r) => (
                <tr key={r.id} style={{ borderTop: '1px solid #f1f5f9' }}>
                  <td style={{ padding: '12px 20px', fontWeight: 500 }}>{r.name}</td>
                  <td style={{ padding: '12px 20px', color: '#64748b' }}>{r.email}</td>
                  <td style={{ padding: '12px 20px' }}>
                    <span style={{ padding: '4px 10px', borderRadius: 999, fontSize: 12, fontWeight: 500, background: r.status === 'Active' ? '#dcfce7' : r.status === 'Pending' ? '#fef9c3' : '#fee2e2', color: r.status === 'Active' ? '#16a34a' : r.status === 'Pending' ? '#ca8a04' : '#dc2626' }}>{r.status}</span>
                  </td>
                  <td style={{ padding: '12px 20px', fontWeight: 600 }}>{r.amount}</td>
                  <td style={{ padding: '12px 20px', display: 'flex', gap: 4 }}>
                    <button style={{ background: 'none', border: 'none', cursor: 'pointer', padding: 4 }}><Eye size={16} color="#94a3b8" variant="Linear" /></button>
                    <button style={{ background: 'none', border: 'none', cursor: 'pointer', padding: 4 }}><Edit size={16} color="#94a3b8" variant="Linear" /></button>
                    <button style={{ background: 'none', border: 'none', cursor: 'pointer', padding: 4 }}><Trash size={16} color="#94a3b8" variant="Linear" /></button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </section>
      </main>
    </div>
  );
}
EOF
echo written; ls -la /Users/faeez/faeez.c/Dashboard.jsx 2>/dev/null