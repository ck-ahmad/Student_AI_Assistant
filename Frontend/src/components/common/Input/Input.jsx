import "./Input.css";

export default function Input({
  label,
  placeholder,
  type = "text",
  value,
  onChange,
  name,
  required = false,
  error = "",
}) {
  return (
    <div className="input-group">
      {label && (
        <label htmlFor={name} className="input-label">
          {label} {required && <span className="required">*</span>}
        </label>
      )}

      <input
        id={name}
        name={name}
        type={type}
        value={value}
        onChange={onChange}
        placeholder={placeholder}
        required={required}
        className={`input-field ${error ? "input-error" : ""}`}
      />

      {error && <small className="error-text">{error}</small>}
    </div>
  );
}
