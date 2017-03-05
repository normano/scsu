#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from scsu import SCSUEncoder


def test_encodings(language: str, text: str):
    print('{0:s} LANGUAGE TEXT:'.format(language.upper()))
    for encoding in ('UTF-8', 'UTF-16BE', 'UTF-32BE', 'GB18030'):
        encoded_text = text.encode(encoding)
        print('\tIN {0:s}: {1:d} byte(s)'.format(encoding, len(encoded_text)))
    e = SCSUEncoder()
    e.train(text)
    b = e.encode(text)
    print('\tIN {0:s}: {1:d} byte(s)'.format('SCSU', len(b)))
    print('')


# Define a list of example sentences.
# (We use the first sentence from the Wikipedia article for "Unicode".)
example_sentences = [
    ('Mandarin', '統一碼是電腦科學領域裡的一項業界標準。'),
    ('Spanish', 'Unicode es un estándar de codificación de caracteres diseñado para facilitar el tratamiento '
                'informático, transmisión y visualización de textos de múltiples lenguajes y disciplinas técnicas,'
                'además de textos clásicos de lenguas muertas.'),
    ('English', 'Unicode is a computing industry standard for the consistent encoding, representation, and handling '
                'of text expressed in most of the world\'s writing systems.'),
    ('Hindi', 'यूनिकोड प्रत्येक अक्षर के लिए एक विशेष संख्या प्रदान करता है, चाहे कोई भी कम्प्यूटर प्लेटफॉर्म, '
              'प्रोग्राम अथवा कोई भी भाषा हो।'),
    ('Arabic', 'في علم الحاسوب، الترميز الموحد (يونيكود أو يُونِكُود) معيار يمكن الحواسيب من تمثيل النصوص المكتوبة '
               'بأغلب نظم الكتابة ومعالجتها، بصورة متناسقة.'),
    ('Portuguese', 'Unicode é um padrão que permite aos computadores representar e manipular, de forma consistente, '
                   'texto de qualquer sistema de escrita existente.'),
    ('Bengali', 'ইউনিকোড একটি আন্তর্জাতিক বর্ণ সংকেতায়ন ব্যবস্থা।'),
    ('Russian', 'Юнико́д — стандарт кодирования символов, позволяющий представить знаки почти всех письменных языков.'),
    ('Japanese', 'ユニコードとは、符号化文字集合や文字符号化方式などを定めた、文字コードの業界規格である。'),
    ('Punjabi', 'ਯੂਨੀਕੋਡ ਹਰ ਇੱਕ ਅੱਖਰ ਲਈ ਇੱਕ ਵਿਸ਼ੇਸ਼ ਗਿਣਤੀ ਪ੍ਰਦਾਨ ਕਰਦਾ ਹੈ, ਚਾਹੇ ਕੋਈ ਵੀ ਕੰਪਿਊਟਰ ਪਲੇਟਫਾਰਮ, ਪ੍ਰੋਗਰਾਮ ਅਤੇ'
                'ਕੋਈ ਵੀ ਭਾਸ਼ਾ ਹੋਵੇ।')
]

print('ENCODING TESTS')
print('')

for language, text in example_sentences:
    test_encodings(language, text)
