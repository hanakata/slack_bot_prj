import wikipedia
from slackbot.bot import respond_to

@respond_to('(.*)とは？')
@respond_to('(.*)って何？')
def wiki(message, something):
    response_string = ''
    wikipedia.set_lang('ja')
    search_res = (wikipedia.search('{0}'.format(something)))
    wiki_len = len(search_res)
    if wiki_len >= 1:
        try:
            wiki_page = wikipedia.page(search_res[0])
            response_string = wiki_page.summary
        except:
            try:
                wiki_page = wikipedia.page(search_res[1])
                response_string = wiki_page.summary
            except:
                response_string = '検索時にエラーが発生しました\n'
    else:
        response_string = '該当する項目はありませんでした。\n'
        response_string += 'google先生に聞いてください。\n'
        response_string += 'https://www.google.co.jp\n'
    message.reply(response_string)