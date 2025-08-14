type AuthButtonProps = {
    buttonlabel: string;
    onclick: () => void;
};

export function AuthButton({ buttonlabel, onclick }: AuthButtonProps) {
    return (
        <button
            className=""
            style={{
                background: "#399B9D",
                borderRadius: "12px",
                color: "#ffffff",
                border: "none",
                minWidth: "115px",
                width: "fit-content",
                height: "40px",
                fontSize: "medium"
            }}
            onClick={onclick}
        >
            {buttonlabel}
        </button>
    );
}