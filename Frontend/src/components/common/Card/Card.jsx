import "./Card.css";

export default function Card({ title, children, footer, onClick }) {
  return (
    <div className="card" onClick={onClick}>
      {title && <div className="card-header">{title}</div>}
      <div className="card-body">{children}</div>
      {footer && <div className="card-footer">{footer}</div>}
    </div>
  );
}
