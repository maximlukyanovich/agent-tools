# Artifact sandbox traps

Read before writing to a design source that is an artifact. A Design System's
component cards and a Design canvas's artboards run in a sandbox; each trap
below was met on a live project and checked on the canvas.

- **`localStorage` throws.** A prototype that keeps state there needs an
  in-memory stand-in behind a `try`/`catch`.
- **No fullscreen, no new tabs.** A prototype that asks for either gets
  nothing; show the state inline.
- **External images do not load.** Demo images go as files beside the
  prototype, their path built from where the bundle was loaded, not written
  out.
- **Uploads belong to one artifact.** An upload's id is its artifact's own,
  and a `/_blob/` URL does not carry into the canvas's copy of the system —
  refer to files by their published path.
- **A file page inside an iframe runs no scripts.** A canvas made as a page
  with a grid of iframes stays blank; one frame is one artboard.
