const API_BASE = 'http://localhost:5000/api';

export const honeypotAPI = {
  async getAttacks() {
    try {
      const response = await fetch(`${API_BASE}/attacks`);
      const data = await response.json();
      return data.attacks || [];
    } catch (error) {
      console.warn('API not available, using demo data');
      return getMockAttacks();
    }
  },

  async getStats() {
    try {
      const response = await fetch(`${API_BASE}/stats`);
      return await response.json();
    } catch (error) {
      return getMockStats();
    }
  }
};

function getMockAttacks() {
  return [
    {
      id: 1,
      timestamp: new Date().toISOString(),
      type: 'SSH Brute Force',
      source_ip: '192.168.1.100',
      details: 'Multiple login attempts',
      honeypot: 'ssh-honeypot'
    }
  ];
}

function getMockStats() {
  return {
    totalAttacks: 0,
    attacksToday: 0,
    uniqueAttackers: 0,
    honeypotsActive: 5,
    threatLevel: 'Low'
  };
}
