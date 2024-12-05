import './button.css'

function MyButton({ onClick, texto, disabled }){
    return(
        <button onClick={onClick} disabled={disabled}>
            {texto}
        </button>
    );
}

export default MyButton;