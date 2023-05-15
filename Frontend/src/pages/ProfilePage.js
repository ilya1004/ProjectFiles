import { Button } from "react-bootstrap";

function ProfilePage() {
  return (
    <div className="prof-page">
      <div className="personal-data">
        <div className="visual-information">
          <div className="profile-avatar">Avatar</div>
          <div className="stat-boxes">
            <ul className="stats">
              <li>Nickname</li>
              <li>Game counter</li>
              <li>Average rate</li>
            </ul>
          </div>
        </div>
        <div className="settings-buttons">
          <Button>Change Nickname</Button>
          <Button>Change Avatar</Button>
        </div>
        <div className="settings-buttons">
          <Button>Personal account settings</Button>
          <Button>Quit the account</Button>
        </div>
      </div>
      <div className="game-statistics">
        <h3>My statistics</h3>
        <table>
          <tr>
            <td>Blitz rating</td>
            <td>Blitz rating</td>
            <td>Blitz rating</td>
          </tr>
          <tr>
            <td>Rapid rating</td>
            <td>Rapid rating</td>
            <td>Rapid rating</td>
          </tr>
          <tr>
            <td>Bullet rating</td>
            <td>Bullet rating</td>
            <td>Bullet rating</td>
          </tr>
        </table>
        <h3 className="stat-header">Match history</h3>
        <table className="match-history">
          <tr>
            <th>Outcome</th>
            <th>Opponent</th>
            <th>Rate change</th>
            <th>Mode</th>
          </tr>
          <tr>
            <td>1</td>
            <td>1</td>
            <td>1</td>
            <td>1</td>
          </tr>
        </table>
      </div>
    </div>
  );
}

export default ProfilePage;
