import fetch from './fetch';

export default (clb = () => {}) => {
    fetch(`http://13.209.247.208:5000/tweet/hot-now`)
        .then((res) => res.json())
        .then((response) => {
            clb(response);
        })
        .catch(() => console.log("Failed to get data."));
};