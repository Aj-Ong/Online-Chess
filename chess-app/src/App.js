import Square from './Square';
import io from 'socket.io-client';

export const socket = io('http://localhost:5000/');

function App() {
  return (
    <div >
      <Square/>
    </div>
  );
}

export default App;
