import {useState} from "react";
import axios, { formToJSON } from 'axios';

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

    axios.get("http://127.0.0.1:5000").then((response) => {
        console.log(response.data);
    });

    async function buscaHeuristica() {
        await gerarMatriz3x3();
        const novaMatriz = localPecas;
        console.log(novaMatriz);
        try {
            const response = await axios.post("http://127.0.0.1:5000/busca-heuristica", {matriz: formToJSON(localPecas)});
            console.log(response.data);
        } catch (error) {
            console.error("Erro ao buscar dados:", error);
        }
    }

    function selectPeca(id){
        setPecaSelecionada(id);
        console.log(`Peça selecionada ${id}`);
        const [pecaClicada, pecaNove] = isNeighbor(id);
        move(pecaClicada, pecaNove);
    }

    function move(pecaClicada, pecaNove) {
        const [i1, j1] = pecaClicada;
        const [i2, j2] = pecaNove;
        if (i1 === null || j1 === null || i2 === null || j2 === null) {
            console.log("Esta casa não é vizinha do 9");
            return;
        }
        const novaMatriz = [...localPecas.map(row => [...row])];
        const temp = novaMatriz[i1][j1];
        novaMatriz[i1][j1] = novaMatriz[i2][j2];
        novaMatriz[i2][j2] = temp;
        setLocalPecas(novaMatriz);
        console.log("Movimento realizado:", novaMatriz);
    }    

    function isNeighbor(id){
        for(let i = 0; i < localPecas.length; i++){
            for(let j = 0; j< localPecas[i].length; j++){
                if(localPecas[i][j] === id){
                    for(let x = 0; x < localPecas.length; x++){
                        for(let y = 0; y < localPecas[x].length; y++){
                            if(localPecas[x][y] === 0){
                                if(x - i === 0 && y - j === 1){
                                    console.log("esquerda")
                                    return[[i, j], [x, y]]
                                }else if(x - i === 0 && y - j === -1){
                                    console.log("direita")
                                    return[[i, j], [x, y]]
                                }else if(x - i === -1 && y - j === 0){
                                    console.log("baixo")
                                    return[[i, j], [x, y]]
                                }else if(x - i === 1 && y - j === 0){
                                    console.log("cima")
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
        setLocalPecas(matriz);
        setIsDisable(true);
    }

    return(
        <>
            <div className="quebraCabeca">
                {localPecas.flat().map((value, index) => (
                    <div key={index} className="peca" id={`peca${value}`} onClick={value !== null ? () => selectPeca(value) : null}>{value !== null ? value : ""}</div>
                ))}
            </div>
            <div>
                <MyButton onClick={() => gerarMatriz3x3()} texto={"Na mão"} disabled={isDisable}/>
                <MyButton onClick={() => buscaHeuristica()} texto={"Algoritmo X"} disabled={isDisable}/>
                <MyButton texto={"Algoritmo Y"} disabled={isDisable}/>
            </div>
            <MyButton onClick={() => verify()} texto={"Verificar vitória"}/>
        </>
    );
}

export default MyGrid;