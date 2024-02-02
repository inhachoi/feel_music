const handleResize = () => {
    const globalBg = document.querySelector('.global-bg');
    let claHeight = globalBg.scrollHeight - window.innerHeight;
    globalBg.style.height = `calc(100vh + ${claHeight}px)`
}
handleResize();
window.addEventListener('resize', handleResize);
