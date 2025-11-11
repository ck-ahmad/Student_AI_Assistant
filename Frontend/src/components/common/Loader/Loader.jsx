import "./Loader.css";

export default function Loader({ size = "medium", fullscreen = false }) {
  const loader = (
    <div className={`loader loader-${size}`}>
      <div className="spinner"></div>
    </div>
  );

  if (fullscreen) {
    return (
      <div className="loader-overlay">
        {loader}
      </div>
    );
  }

  return loader;
}
