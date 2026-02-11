import React, { useState, useEffect } from 'react';

const Leaderboard = () => {
  const [leaderboard, setLeaderboard] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const apiBaseUrl = `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api`;

  useEffect(() => {
    fetchLeaderboard();
  }, []);

  const fetchLeaderboard = async () => {
    try {
      const apiUrl = `${apiBaseUrl}/leaderboard/`;
      const response = await fetch(apiUrl);
      if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
      const data = await response.json();
      setLeaderboard(Array.isArray(data.results || data) ? (data.results || data) : []);
      setLoading(false);
    } catch (err) {
      setError(err.message);
      setLoading(false);
    }
  };

  if (loading) return <div className="container mt-5 text-center"><div className="spinner-border" role="status"></div></div>;
  if (error) return <div className="container mt-5"><div className="alert alert-danger">Error: {error}</div></div>;

  return (
    <div className="container mt-4">
      <h2>Leaderboard</h2>
      <div className="table-responsive">
        <table className="table table-striped table-hover">
          <thead>
            <tr>
              <th>Rank</th>
              <th>User</th>
              <th>Team</th>
              <th>Total Calories</th>
              <th>Activities</th>
            </tr>
          </thead>
          <tbody>
            {leaderboard.map((entry, index) => (
              <tr key={entry.id || index}>
                <td>{index + 1}</td>
                <td>{entry.user_name || entry.user}</td>
                <td>{entry.team}</td>
                <td>{entry.total_calories || 0}</td>
                <td>{entry.activity_count || 0}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <p className="text-muted">Total entries: {leaderboard.length}</p>
    </div>
  );
};

export default Leaderboard;
