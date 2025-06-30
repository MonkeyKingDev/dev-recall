function log_devrecall() {
  python3 /absolute/path/to/main.py log "$1"
}

precmd() {
  log_devrecall "$(fc -ln -1)"
}
