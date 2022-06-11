import fetch from './fetch';

export default (keyword, term, clb = () => {}) => {
    fetch(`http://13.209.247.208:5000/tweet/count?query=${keyword}&granularity=${term == 1 ? "hour" : "day"}`)
        .then((res) => res.json())
        .then((response) => {
            clb(response);
        })
        .catch(() => console.log("Failed to get data."));
};