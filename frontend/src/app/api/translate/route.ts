import { NextResponse } from 'next/server';

export async function POST(request: Request) {
  try {
    const { texts, targetLang } = await request.json();

    if (!texts || !targetLang) {
      return NextResponse.json({ error: 'Missing texts or targetLang' }, { status: 400 });
    }

    if (targetLang === 'en') {
      const result: Record<string, string> = {};
      Object.keys(texts).forEach(key => {
        result[key] = texts[key];
      });
      return NextResponse.json({ translations: result });
    }

    const keys = Object.keys(texts);
    const values = Object.values(texts) as string[];

    // Using a safe delimiter to batch translate all strings at once 
    const delimiter = ' [X_DELIMIT_X] ';
    const joinedText = values.join(delimiter);

    // Using the free Google Translate API endpoint via native fetch
    const url = `https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl=${targetLang}&dt=t&q=${encodeURIComponent(joinedText)}`;
    
    const res = await fetch(url);
    const data = await res.json();

    // The free API returns an array of arrays, where the first element contains the translated segments
    let translatedJoinedText = '';
    if (data && data[0]) {
      translatedJoinedText = data[0].map((item: any) => item[0]).join('');
    } else {
      throw new Error('Invalid response from translation service');
    }

    // Using regex to handle potential formatting changes by the translator
    const translatedValues = translatedJoinedText.split(/\[\s?X_DELIMIT_X\s?\]/i).map((s: string) => s.trim());

    const result: Record<string, string> = {};
    keys.forEach((key, index) => {
      result[key] = translatedValues[index] || values[index];
    });

    return NextResponse.json({ translations: result });

  } catch (error: any) {
    console.error('Translation API Error:', error);
    return NextResponse.json({ error: error.message || 'Translation failed' }, { status: 500 });
  }
}
