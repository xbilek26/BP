## Cíle, kterých má být dosaženo
Student nastuduje a teoreticky popíše současné metody detekce anomálií (například odstranění/přidání/přemístění objektu) ve videosekvencích na zařízeních s nízkým výkonem, tedy na zařízení disponujícím pouze procesorem s maximálně čtyřmi jádry. Vybrané metody implementuje ve vlastní samostatné aplikaci, která bude umožňovat načtení videa ke zpracování, detekci anomálií a vhodnou interpretaci výsledků. V rámci semestrální práce je požadováno vytvoření aplikace se základním ovládacím rozhraním a vytvoření algoritmu pro jednoduchou detekci anomálií.

## Výsledky

Zejména na druhé ukázce je vidět, že algoritmus je schopen detekovat anomálie typu odstanění nebo poškození objektu. NN byla natrénována a reaguje na případy, kdy
- útočník viditělně poškozuje objekt na videu (zde konkrétně páčení kapoty a její poškození)
- zloděj odebírá nějaký objekt (ukradení auta)

test_1.mp4             |  test_2.mp4
:-------------------------:|:-------------------------:
![test.mp4 preview](https://github.com/xbilek26/BP/blob/main/output_preview/test_1.gif)  |  ![test_2.mp4 preview](https://github.com/xbilek26/BP/blob/main/output_preview/test_2.gif)
