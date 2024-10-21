export const readFromFile = (file, callback) => {
  const reader = new FileReader();
  reader.onload = (event) => {
    const content = event.target.result;
    callback(content);
  };
  reader.readAsText(file);
};

export const substituteLetters = (str, original, substitute) => {
  return str.split(original).join(substitute);
};

export const findFrequency = (str) => {
  const frequency = {};
  for (let char of str) {
    if (char.match(/[A-Z]/)) {
      frequency[char] = (frequency[char] || 0) + 1;
    }
  }
  return frequency;
};
