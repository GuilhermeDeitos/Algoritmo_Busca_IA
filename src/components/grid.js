import {useState} from "react";

import MyButton from './button';

import './grid.css'

function MyGrid(){
    const correctAnswer = [
        [1,2,3],
        [4,5,6],
        [7,8,9]
    ]

    const initialLocalPecas = [
        [0,0,0],
        [0,0,0],
        [0,0,0]
    ];

    const [localPecas, setLocalPecas] = useState(initialLocalPecas);
    const [pecaSelecionada, setPecaSelecionada] = useState(null);

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
                if(localPecas[i][j] == id){
                    for(let x = 0; x < localPecas.length; x++){
                        for(let y = 0; y < localPecas[x].length; y++){
                            if(localPecas[x][y] == 9){
                                if(x - i == 0 && y - j == 1){
                                    console.log("esquerda")
                                    return[[i, j], [x, y]]
                                }else if(x - i == 0 && y - j == -1){
                                    console.log("direita")
                                    return[[i, j], [x, y]]
                                }else if(x - i == -1 && y - j == 0){
                                    console.log("baixo")
                                    return[[i, j], [x, y]]
                                }else if(x - i == 1 && y - j == 0){
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
            setLocalPecas(initialLocalPecas);
        }else{
            alert("posicione as peças na ordem correta!")
        }
    }

    function gerarMatriz3x3() {
        const numeros = Array.from({ length: 9 }, (_, i) => i + 1);
        for (let i = numeros.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [numeros[i], numeros[j]] = [numeros[j], numeros[i]];
        }
        const matriz = [];
        for (let i = 0; i < 3; i++) {
            matriz.push(numeros.slice(i * 3, i * 3 + 3));
        }
        setLocalPecas(matriz);
        console.log("teste")
    }

    return(
        <>
            <div className="quebraCabeca" aria-disabled>
                {localPecas.flat().map((value, index) => (
                    <div key={index} className="peca" id={`peca${value}`} onClick={value !== 0 && value !== 9 ? () => selectPeca(value) : null}>{value !== 0 ? value : ""}</div>
                ))}
            </div>
            <div>
                <MyButton onClick={() => gerarMatriz3x3()}texto={"Na mão"}/>
                <MyButton texto={"Algoritmo X"}/>
                <MyButton texto={"Algoritmo Y"}/>
            </div>
            <MyButton onClick={() => verify()} texto={"Verificar vitória"}/>
        </>
    );
}

export default MyGrid;