import asyncio
import os.path
import typing

import nodriver as chrome_browser

import nodriver.cdp.dom
import nodriver.core.element

from nodriver.core.config import (
    Config as ChromeBrowserConfig
)

from nodriver.core.util import (
    filter_recurse_all
)


_DATA_DIRECTORY_PATH = (
    './'
    'data/'
)

_COOKIES_FILE_PATH = (
    _DATA_DIRECTORY_PATH +
    'cookies.dat'
)

_CV_NAMES = [
    # 'Старший разработчик',
    # 'Инженер-программист'
    'Разработчик Python',
    'Senior Python Developer',
    'Python Developer'
]

_CV_RAISE_BUTTON_TEXT = (
    'Поднять в поиске'
)


async def main() -> None:
    browser_config = (
        ChromeBrowserConfig(
            browser_args=[
                # '--disable-web-security',
                # '--user-agent=ChromeHeadless'  # (for CF testing)
                # f'--user-agent={browser_user_agent}'
            ],

            headless=(
                # True  # TODO
                False
            )
        )
    )

    browser = (
        await (
            chrome_browser.start(
                browser_config
            )
        )
    )

    await (
        browser
    )

    if (
            os.path.exists(
                _COOKIES_FILE_PATH
            )
    ):
        await (
            browser.cookies.load(
                _COOKIES_FILE_PATH
            )
        )

    main_page = (
        await (
            browser.get(
                'https://hh.ru/applicant/resumes'
                '?from_delete=true'
            )
        )
    )

    await (
        main_page
    )

    await (
        asyncio.sleep(
            1.0  # s
        )
    )

    while True:
        await (
            main_page
        )

        for cv_name in (
                _CV_NAMES
        ):
            print(f'cv_name: {cv_name!r}')

            cv_block_elements = (
                await (
                    main_page.find_elements_by_text(
                        text=(
                            cv_name
                        )
                    )
                )
            )

            print(f'- len(cv_block_elements): {len(cv_block_elements)}')

            is_cv_button_clicked = (
                False
            )

            for cv_block_element in (
                    cv_block_elements
            ):
                if (
                        cv_block_element.tag_name !=
                        'div'
                ):
                    continue

                cv_span_elements: (
                    typing.List[
                        typing.Union[
                            nodriver.cdp.dom.Node,
                            nodriver.core.element.Element
                        ]
                    ]
                ) = (
                    filter_recurse_all(
                        cv_block_element,

                        lambda node: (  # TODO: move to function  # noqa
                            (
                                node.node_type ==
                                1
                            ) and

                            (
                                node.tag_name ==
                                'span'
                            ) and

                            (
                                node.text ==
                                _CV_RAISE_BUTTON_TEXT
                            )
                        )
                    )
                )

                for cv_span_element in (
                        cv_span_elements
                ):
                    print(
                        '- - cv_span_element'
                        f': {cv_span_element}'
                    )

                    print(
                        '- - Clicking...'
                    )

                    await (
                        cv_span_element.click()
                    )

                    print(
                        '- - Clicked.'
                    )

                    is_cv_button_clicked = (
                        True
                    )

                    await (
                        asyncio.sleep(
                            5.0  # s
                        )
                    )

                    await (
                        main_page.reload()
                    )

                    await (
                        asyncio.sleep(
                            5.0  # s
                        )
                    )

                    break

                if is_cv_button_clicked:
                    break

        await (
            browser.cookies.save(
                _COOKIES_FILE_PATH
            )
        )

        await (
            asyncio.sleep(
                60.0 *  # s
                1.0     # m
            )
        )


if __name__ == '__main__':
    asyncio.run(
        main()
    )
