import { useState } from "react";
import axios from "axios";
import MyButton from "./button";
import "./grid.css";

function MyGridManual() {
  const correctAnswer = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 0],
  ];

  const initialLocalPecas = [
    [null, null, null],
    [null, null, null],
    [null, null, null],
  ];

  const [localPecas, setLocalPecas] = useState(initialLocalPecas);
  const [pecaSelecionada, setPecaSelecionada] = useState(null);
  const [isDisable, setIsDisable] = useState(false);

  // Função para definir peças manualmente
  function handleInputChange(value, i, j) {
    const novaMatriz = [...localPecas.map((row) => [...row])];
    novaMatriz[i][j] = value !== "" ? parseInt(value) : null;
    setLocalPecas(novaMatriz);
  }

  async function buscaHeuristica() {
    try {
      const response = await axios.post("http://127.0.0.1:5000/busca-heuristica", {
        matriz: JSON.stringify(localPecas),
      });
      move_buscas(response.data["caminho"]);
    } catch (error) {
      console.error("Erro ao buscar dados:", error.response?.data || error);
      alert(error.response?.data?.erro || "Erro desconhecido.");
      setLocalPecas(initialLocalPecas);
      setIsDisable(false);
    }
  }

  async function buscaCega() {
    try {
      const response = await axios.post("http://127.0.0.1:5000/busca-cega", {
        matriz: JSON.stringify(localPecas),
      });
      move_buscas(response.data["caminho"]);
    } catch (error) {
      console.error("Erro ao buscar dados:", error.response?.data || error);
      alert(error.response?.data?.erro || "Erro desconhecido.");
      setLocalPecas(initialLocalPecas);
      setIsDisable(false);
    }
  }

  async function move_buscas(matriz) {
    for (let i = 0; i < matriz.length; i++) {
      setLocalPecas(matriz[i]);
      await new Promise((resolve) => setTimeout(resolve, 500));
    }
  }

  function selectPeca(id){
    setPecaSelecionada(id);
    const [pecaClicada, pecaNove] = isNeighbor(id);
    move(pecaClicada, pecaNove);
}

  function move(pecaClicada, pecaNove) {
    const [i1, j1] = pecaClicada;
    const [i2, j2] = pecaNove;
    if (i1 === null || j1 === null || i2 === null || j2 === null) {
        return;
    }
    const novaMatriz = [...localPecas.map(row => [...row])];
    const temp = novaMatriz[i1][j1];
    novaMatriz[i1][j1] = novaMatriz[i2][j2];
    novaMatriz[i2][j2] = temp;
    setLocalPecas(novaMatriz);
}    

  function isNeighbor(id){
    for(let i = 0; i < localPecas.length; i++){
        for(let j = 0; j< localPecas[i].length; j++){
            if(localPecas[i][j] === id){
                for(let x = 0; x < localPecas.length; x++){
                    for(let y = 0; y < localPecas[x].length; y++){
                        if(localPecas[x][y] === 0){
                            if(x - i === 0 && y - j === 1){
                                return[[i, j], [x, y]]
                            }else if(x - i === 0 && y - j === -1){
                                return[[i, j], [x, y]]
                            }else if(x - i === -1 && y - j === 0){
                                return[[i, j], [x, y]]
                            }else if(x - i === 1 && y - j === 0){
                                return[[i, j], [x, y]]
                            }else{
                                return[[null, null], [null, null]]
                            }
                        }
                    }
                }
            }
        }
    }

}

function verify(){
    const venceu = JSON.stringify(localPecas) === JSON.stringify(correctAnswer);
    if(venceu){
        alert("vc venceu")
        setIsDisable(false);
        setLocalPecas(initialLocalPecas);
    }else{
        alert("posicione as peças na ordem correta!")
    }
}

  return (
    <>
      <div className="inputGrid">
        {localPecas.map((row, i) =>
          row.map((value, j) => (
            <input
              key={`${i}-${j}`}
              type="number"
              min={0}
              max={8}
              value={value ?? ""}
              onChange={(e) => handleInputChange(e.target.value, i, j)}
              className="gridInput"
              disabled={isDisable}
            />
          ))
        )}
      </div>

      <div className="quebraCabeca">
        {localPecas.flat().map((value, index) => (
          <div
            key={index}
            className="peca"
            id={`peca${value}`}
            onClick={value !== null ? () => selectPeca(value) : null}
          >
            {value !== null ? value : ""}
          </div>
        ))}
      </div>

      <div>
        <MyButton onClick={buscaHeuristica} texto={"A*"} disabled={isDisable} />
        <MyButton onClick={buscaCega} texto={"Profundidade Iterativa"} disabled={isDisable} />
      </div>
      <MyButton onClick={verify} texto={"Verificar vitória"} />
    </>
  );
}

export default MyGridManual;
