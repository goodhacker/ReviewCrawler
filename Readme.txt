������windows�ϲ����ڱ��������ˣ�������è��ҳ����ˣ������һ��Ǹ��Ÿ���һЩ��
�����������ݶ�����utf-8����ʽ�洢��.csv���excel�������롣���Լ���EditPlus�����ı��༭���ĸ���

���ԣ�python2.7  python3����Ŷ

��������⣺
Beautifulsoup4  http://www.crummy.com/software/BeautifulSoup/bs4/download/
twisted  http://twistedmatrix.com/trac/


��Ҫ�ļ���

ReviewCrawler.py 
Ҳ�������ļ�
����ļ���Ҫ�Ƿ�����Ʒ�б���棬�����Ʒ�Ļ�����Ϣ��������Ʒ���ƣ���Ʒid��ͼƬ��ַ����Ǯ�ȡ�Ȼ��ͨ����Щ��Ϣ�ҵ�ĳ��Ʒ��ҳ�档
��������Ʒ��ַ��visited.dat��»ؾͲ�����
���ԸĵĲ����У�
1. �������firstUrl������Ҫ������Ʒ�б�ĵ�ַ�������ַ�����Ա�������ĳ�ؼ��ֺ󣬵���������õĵ�ַ
�������֣�����Ӧ���������ģ�http://s8.taobao.com/search?q=%CA%D6%B1%ED&pid=mm_34012603_3435519_11130749&commend=all&ssid=s5-e
2. �������BASE_INFO_FILE��BASE_INFO_PATH���Ǵ洢��Ʒ������Ϣ��������⣬��Ǯ��ͼƬ��ַ�ȣ��ļ���ַ
3. ITEM_NUM Ҫ������Ʒ���������40��һҳ����40����

BaseReviewCrawler.py
�Ա�����è���Ա����ֵ꣬�����ǲ�һ���ģ�����һЩ�������������url��д���ļ�ʲô�Ĳ�������BaseReviewCrawler�
��ҳ����صĶ���SubReviewCrawler��
���ԸĵĲ�����
1. CSV_PATH  csv�ļ���ַ
2. writeToCSV��������csvд��ʲô��Ϣ�Ĵ���fieldnames����Ϣ���б���

SubReviewCrawler.py
��Taobao��Tmall������
���Ըĵģ�
1. TIMEOUT����λs,�������ʱ�����ҳ�������
2. ÿ�����self.jsonPath��json�ļ��Ĵ洢λ�ã�������Ҫ��json��������鲻Ҫ��ɾ
3. ÿ�����parseReviewJson�������������۵�json�ļ����������ӣ�
tmall��http://rate.tmall.com/list_detail_rate.htm?itemId=8140241528&spuId=123185051&sellerId=525798483&order=0&forShop=1&_ksTS=1366450096661_1004&callback=jsonp1005
taobao��http://rate.taobao.com/feedRateList.htm?callback=jsonp_reviews_list&userNumId=811030409&auctionNumId=15043528059&siteID=7&currentPageNum=1&rateType=&orderType=sort_weight&showContent=1&attribute=

DictUnicodeWriter.py
д��CSV���̵ķ�װ���������ù�

removeDuplicate.py
��Ҳ��֪��Ϊʲô��ʱ����ظ�����������һ��������С�����ĵ�ַ�ĳ�csv���ڵ�ַ

�����ļ�����

��Ϊ�г�ʱ�쳣�������Ի�����������˿����ܾ��С����������ط�ûץ�쳣�����Ա��˾�ֻ�ܸĴ����ˡ�