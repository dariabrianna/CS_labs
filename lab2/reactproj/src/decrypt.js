import React, { useState } from "react";
import BarChart from "./BarChart"; // Import the BarChart component
import { readFromFile, substituteLetters, findFrequency } from "./utils"; // Utility functions

const DecryptorApp = () => {
  // Predefine the alphabet substitution mapping
  const initialSubstitutions = {
    'V': 'e',
    'W': 't',
    'Q': 'h',
    'N': 'o',
    'C': 'f',
    'G': 'n',
    'X': 'i',
    'P': 's',
    'O': 'd',
    'I': 'r',
    'L': 'k',
    'H': 'c',
    'J': 'g',
    'M': 'z',
    'Z': 'm',
    'U': 'p',
    'D': 'u',
    'F': 'y',
    'S': 'l',
    'K': 'v',
    'A': 'b',
    'R': 'w',
    'Y': 'x',
    'B': 'q',
    'E': 'j',
    'T': 'a',
  };

  const [encryptedText, setEncryptedText] = useState("");
  const [decryptedText, setDecryptedText] = useState("");
  const [letterSubstitutions, setLetterSubstitutions] = useState(initialSubstitutions); // Initialize with predefined alphabet
  const [frequencyData, setFrequencyData] = useState({});

  const handleFileUpload = (e) => {
    const file = e.target.files[0];
    readFromFile(file, (content) => {
      setEncryptedText(content.toUpperCase());
    });
  };

  // Update individual substitutions if needed
  const handleSubstitutionChange = (original, substitute) => {
    setLetterSubstitutions({ ...letterSubstitutions, [original]: substitute });
  };

  const handleDecrypt = () => {
    let decrypted = encryptedText;
    Object.entries(letterSubstitutions).forEach(([original, substitute]) => {
      decrypted = substituteLetters(decrypted, original, substitute);
    });
    setDecryptedText(decrypted);

    // Generate frequency data
    const frequency = findFrequency(decrypted);
    const frequencyLabels = Object.keys(frequency);
    const frequencyValues = Object.values(frequency);

    // Format data for the BarChart
    setFrequencyData({
      labels: frequencyLabels,
      datasets: [
        {
          label: "Letter Frequency",
          data: frequencyValues,
          backgroundColor: "rgba(75,192,192,0.6)",
          borderColor: "rgba(75,192,192,1)",
          borderWidth: 1,
        },
      ],
    });
  };

  const handleTextInputChange = (e) => {
    setEncryptedText(e.target.value.toUpperCase());
  };

  return (
    <div>
      <h1>Decryption Tool</h1>

      {/* Option to upload a file */}
      <input type="file" accept=".txt" onChange={handleFileUpload} />

      {/* Option to manually input encrypted text */}
      <div>
        <h3>Or input text to decrypt:</h3>
        <textarea
          value={encryptedText}
          onChange={handleTextInputChange}
          rows="10"
          cols="50"
          placeholder="Input encrypted text here"
        />
      </div>

      <div>
        <h3>Substitutions:</h3>
        {Object.keys(letterSubstitutions).map((letter) => (
          <div key={letter}>
            <label>{letter} to:</label>
            <input
              type="text"
              maxLength={1}
              value={letterSubstitutions[letter]} // Pre-fill with the predefined value
              onChange={(e) => handleSubstitutionChange(letter, e.target.value)}
            />
          </div>
        ))}
      </div>

      <button onClick={handleDecrypt}>Decrypt</button>

      {/* Display the decrypted text */}
      <textarea value={decryptedText} readOnly rows="10" cols="50" />

      {/* Render BarChart if frequencyData is available */}
      {frequencyData && frequencyData.labels && (
        <BarChart data={frequencyData} />
      )}
    </div>
  );
};

export default DecryptorApp;
