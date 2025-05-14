const updateTime = () => {
    let date = new Date();
   
    let secToDeg = (date.getSeconds() / 60) * 360;
    let minToDeg = (date.getMinutes() / 60) * 360;
    let hrToDeg = (date.getHours() / 12) * 360;

    document.querySelector(".clock-second").style.transform = `rotate(${secToDeg}deg)`;
    document.querySelector(".clock-minute").style.transform = `rotate(${minToDeg}deg)`;
    document.querySelector(".clock-hour").style.transform = `rotate(${hrToDeg}deg)`;
};

setInterval(updateTime, 1000);
updateTime();