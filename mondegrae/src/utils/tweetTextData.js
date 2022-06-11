import fetch from './fetch';

export default (keyword, date, clb = () => {}) => {
    fetch(`http://13.209.247.208:5000/tweet/?query=${keyword}&time=${date}`)
        .then((res) => res.json())
        .then((response) => {
            clb(response);
        })
        .catch(() => console.log("Failed to get data."));
};