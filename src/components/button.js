import './button.css'

function MyButton({ onClick, texto }){
    return(
        <button onClick={onClick}>
            {texto}
        </button>
    );
}

export default MyButton;