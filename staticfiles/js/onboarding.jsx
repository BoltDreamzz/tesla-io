const { useState } = React;

function Onboarding() {

    const slides = [

        {
            title: "Cutting Edge Finance with QFS.",

            subtitle:
                "Secure your funds through our super smart algorithms specifically created for crypto and bank assets.",

            image: "/static/svg/001.svg",

            button: "Next"
        },

        {
            title: "Military Grade Security Approach.",

            subtitle:
                "Your transactions are encrypted and protected with military type security at all times.",

            image: "/static/home_media/security.svg",

            button: "Next"
        },

        {
            title: "Start Securing your Assets in few clicks.",

            subtitle:
                "Let's begin your financial journey with QFX.",

            image: "/static/home_media/rocket.svg",

            button: "Done"
        }

    ];

    const [current, setCurrent] = useState(0);

    const slide = slides[current];

    function next() {

        if (current < slides.length - 1) {

            setCurrent(current + 1);

        }
        else {

            alert("Redirecting...");

            window.location = "../qfs/cards/";

        }

    }

    function previous() {

        if (current > 0) {

            setCurrent(current - 1);

        }

    }

    function skip() {

        setCurrent(slides.length - 1);

    }

    function playAgain() {

        setCurrent(0);

    }

    return (

        <div
            className="h-screen w-screen flex items-center justify-center bg-gradient-to-br from-slate-950 via-blue-950 to-slate-900 overflow-hidden">

            <div
                className="w-full max-w-4xl h-[75vh] rounded-3xl bg-white/10 backdrop-blur-xl shadow-2xl border border-white/20 p-4 flex flex-col items-center justify-center">

                {/* Image */}

                {/* <div
                    className="flex justify-center ">

                    <img

                        src={slide.image}

                        className="w-[180px] object-cover" />

                </div> */}

                {/* Title */}

                <h1
                    className="text-center text-white text-7xl font-bold mt-auto">

                    {slide.title}

                </h1>

                <p
                    className="text-center text-slate-300 mt-6 text-xl">

                    {slide.subtitle}

                </p>

                {/* Progress */}

                <div
                    className="flex justify-center gap-3 mt-12">

                    {

                        slides.map((item, index) => (

                            <div

                                key={index}

                                className={`

                                    w-3

                                    h-3

                                    rounded-full

                                    transition-all

                                    duration-300

                                    ${index === current

                                        ?

                                        "bg-blue-500 scale-125"

                                        :

                                        "bg-gray-500"

                                    }

`}

                            />

                        ))

                    }

                </div>

                {/* Buttons */}

                <div
                    className="mt-auto flex justify-between text-xl">

                    <div>

                        {

                            current > 0 &&

                            <button

                                onClick={previous}

                                className="px-6 py-3 rounded-xl bg-slate-700 hover:bg-slate-600 text-white">

                                Back

                            </button>

                        }

                    </div>

                    <div
                        className="space-x-3">

                        {

                            current !== slides.length - 1 &&

                            <button

                                onClick={skip}

                                className="px-6 py-3 rounded-xl bg-transparent border border-gray-500 text-gray-300 hover:bg-gray-800">

                                Skip

                            </button>

                        }

                        <button

                            onClick={next}

                            className="px-8 py-3 rounded-xl bg-blue-600 hover:bg-blue-700 text-white">

                            {slide.button}

                        </button>

                    </div>

                </div>

                {

                    current === slides.length - 1 &&

                    <div
                        className="mt-8 text-center">

                        <button

                            onClick={playAgain}

                            className="text-blue-400 hover:text-blue-300">

                            ▶ Play Again

                        </button>

                    </div>

                }

            </div>

        </div>

    );

}

const root =
    document.getElementById("onboarding-root");

if (root) {

    if (!window.onboardingRoot) {

        window.onboardingRoot =
            ReactDOM.createRoot(root);

    }

    window.onboardingRoot.render(
        <Onboarding />
    );

}