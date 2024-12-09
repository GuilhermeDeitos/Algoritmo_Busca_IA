import {useState} from "react";
import axios from 'axios';

import MyButton from './button';

import './grid.css'

function MyGrid(){
    const correctAnswer = [
        [1,2,3],
        [4,5,6],
        [7,8,0]
    ]
    const initialLocalPecas = [
        [null,null,null],
        [null,null,null],
        [null,null,null]
    ];

    const [localPecas, setLocalPecas] = useState(initialLocalPecas);
    const [pecaSelecionada, setPecaSelecionada] = useState(null);
    const [isDisable, setIsDisable] = useState(false);

    function espera(ms){ return new Promise(resolve => setTimeout(resolve, ms));}

    async function buscaHeuristica() {
        const novaMatriz = gerarMatriz3x3(); // Gere a nova matriz
        setLocalPecas(novaMatriz); // Atualize o estado
        try {
          // Use a matriz gerada diretamente, em vez de confiar no estado
            const response = await axios.post("http://127.0.0.1:5000/busca-heuristica", {matriz : JSON.stringify(novaMatriz)});
            move_buscas(response.data["caminho"]);
        } catch (error) {
            console.error("Erro ao buscar dados:", error.response.data);
            alert(JSON.stringify(error.response.data["erro"]));
            setLocalPecas(initialLocalPecas)
            setIsDisable(false);
        }
    }

    async function buscaCega(){
        const novaMatriz = gerarMatriz3x3();
        setLocalPecas(novaMatriz);
        try {
            const response = await axios.post("http://127.0.0.1:5000/busca-cega", {matriz : JSON.stringify(novaMatriz)});
            move_buscas(response.data["caminho"]);
        }catch (error){
            console.error("Erro ao buscar dados:", error.response.data);
            alert(JSON.stringify(error.response.data["erro"]));
            setLocalPecas(initialLocalPecas)
            setIsDisable(false);
        }
    }

    function naMao(){
        const novaMatriz = gerarMatriz3x3();
        setLocalPecas(novaMatriz);
    }

    async function move_buscas(matriz){
        for(let i = 0; i < matriz.length; i++){
            setLocalPecas(matriz[i]);
            await espera(500);
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

    function gerarMatriz3x3() {
        const numeros = Array.from({ length: 9 }, (_, i) => i);
        for (let i = numeros.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [numeros[i], numeros[j]] = [numeros[j], numeros[i]];
        }
        const matriz = [];
        for (let i = 0; i < 3; i++) {
            matriz.push(numeros.slice(i * 3, i * 3 + 3));
        }
        setIsDisable(true);
        return matriz;
    }

    return(
        <>
            <div className="quebraCabeca">
                {localPecas.flat().map((value, index) => (
                    <div key={index} className="peca" id={`peca${value}`} onClick={value !== null ? () => selectPeca(value) : null}>{value !== null ? value : ""}</div>
                ))}
            </div>
            <div>
                <MyButton onClick={() => naMao()} texto={"Na mão"} disabled={isDisable}/>
                <MyButton onClick={() => buscaHeuristica()} texto={"A*"} disabled={isDisable}/>
                <MyButton onClick={() => buscaCega()} texto={"Profundidade Iterativa"} disabled={isDisable}/>
            </div>
            <MyButton onClick={() => verify()} texto={"Verificar vitória"}/>
        </>
    );
}

export default MyGrid;