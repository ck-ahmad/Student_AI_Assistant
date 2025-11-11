import "./Modal.css";
import Button from "../Button/Button";

export default function Modal({ isOpen, onClose, title, children }) {
  if (!isOpen) return null;

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal" onClick={(e) => e.stopPropagation()}>
        {title && <div className="modal-header">{title}</div>}

        <div className="modal-body">{children}</div>

        <div className="modal-footer">
          {/* ✅ Use common Button instead of raw <button> */}
          <Button variant="secondary" onClick={onClose}>
            Close
          </Button>
        </div>
      </div>
    </div>
  );
}
