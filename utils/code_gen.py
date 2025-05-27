def generate_code_boilerplate(tech_stack):
    tech_stack = tech_stack.lower()

    if "react" in tech_stack:
        return """import React from 'react';

export default function App() {
  return <h1>Hello from AgentOps!</h1>;
}
"""
    elif "flask" in tech_stack:
        return """from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello from AgentOps Flask app!'

if __name__ == '__main__':
    app.run(debug=True)
"""
    elif "node.js" in tech_stack or "express" in tech_stack:
        return """const express = require('express');
const app = express();

app.get('/', (req, res) => {
  res.send('Hello from AgentOps Express app!');
});

app.listen(3000, () => {
  console.log('Server running at http://localhost:3000');
});
"""
    else:
        return "# No boilerplate found for this stack. Try refining your idea or tech keywords."
