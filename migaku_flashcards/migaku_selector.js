(async function clickAllEvenCheckBoxesSmoothly() {
    const clicked = new Set();
    let lastCheckboxCount = 0;
    let unchangedTries = 0;

    const SCROLL_STEP = 500; // pixels per scroll
    const SCROLL_DELAY = 50; // ms wait between scrolls
    const MAX_TRIES_WITHOUT_NEW = 30; // safety exit

    while (unchangedTries < MAX_TRIES_WITHOUT_NEW) {
        // SCROLL DOWN A BIT
        window.scrollBy(0, SCROLL_STEP);
        await new Promise(resolve => setTimeout(resolve, SCROLL_DELAY));

        // CLICK NEWLY LOADED CHECKBOXES
        const checkboxes = document.querySelectorAll('input[type="checkbox"][id^="item-"]');
        let newClicks = 0;

        checkboxes.forEach(cb => {
            const idStr = cb.id.replace('item-', '');
            const idNum = parseInt(idStr);
            if (idNum % 2 === 0 && !clicked.has(idStr)) {
                cb.click();
                clicked.add(idStr);
                newClicks++;
            }
        });

        if (clicked.size === lastCheckboxCount) {
            unchangedTries++;
        } else {
            unchangedTries = 0;
            lastCheckboxCount = clicked.size;
        }

        console.log(`✅ Clicked ${clicked.size} checkboxes so far...`);
    }

    console.log(`🎉 Done. Total even checkboxes clicked: ${clicked.size}`);
})();