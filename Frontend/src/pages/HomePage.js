import "../css/Home.css"

function HomePage() {
    return (
      <div className="home-page">
        <div className="welcome-box">
            <h1>Welcome to Belchessmind.org</h1>
        </div>
        <div className="introduction-box">
            <div className="board-container"><img src="https://upload.wikimedia.org/wikipedia/commons/b/b0/Belarusian_chess_board_with_classical_images_of_pieces.jpg" alt="Error"></img></div>
            <div className="text-container">
                <text className="test-intro"><b>Белорусские шахматы</b> — разновидность шахмат, созданная в Беларуси
                    в 2010 году Александром Островским и Николаем Томашевичем. Основными отличиями
                    игры являются доска на 81 клетку (9х9), наличие трона и дворца.
                    Седьмой фигурой стал княжич, который при определённых условиях может стать князем.
                    Остальные фигуры близки к своим аналогам в традиционных шахматах,
                    но названы в честь исторических белорусских военных единиц.
                </text>
            </div>
        </div>
      </div>
    );
  }
  
  export default HomePage;