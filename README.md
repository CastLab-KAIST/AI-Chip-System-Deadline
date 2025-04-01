## Cast Deadlines

Countdown timers to keep track of a bunch of Computer Architecture/Circuit/Automation/FPGA/AI conference deadlines.

This is a fork of the [ai-deadlines](https://github.com/paperswithcode/ai-deadlines) website.

## Contributing

Contributions are very welcome! We are only looking to list top-tier conferences in AI chip as per [conferenceranks.com][3] and our judgement calls. Please feel free to maintain a separate fork if you don't see your sub-field or conference of interest listed.

To add or update a deadline:
- Fork the repository
- Update `_data/conferences.yml`
- Make sure it has the `title`, `year`, `id`, `link`, `deadline`, `timezone`, `date`, `place`, `sub` attributes
    + See available timezone strings [here](https://momentjs.com/timezone/).
- Optionally add a `note` and `abstract_deadline` in case the conference has a separate mandatory abstract deadline
- Optionally add `hindex` (refers to h5-index from [here](https://scholar.google.com/citations?view_op=top_venues&vq=eng))
- Example:
    ```yaml
    - id: bestconf25  # title as lower case + last two digits of year
      title: BestConf
      year: 2025
      full_name: Best Conference for Anything  # full conference name
      link: link-to-website.com
      abstract_deadline: YYYY-MM-DD HH:SS
      deadline: YYYY-MM-DD HH:SS
      timezone: Asia/Seoul
      place: Incheon, South Korea
      date: September, 18-22, 2025
      start: YYYY-MM-DD
      end: YYYY-MM-DD
      paperslink: link-to-full-paper-list.com
      pwclink: link-to-papers-with-code.com
      hindex: 100.0
      sub: SP
      note: Important
    ```
- Send a pull request

## License

This project is licensed under [MIT][1].

It uses:

- [IcoMoon Icons](https://icomoon.io/#icons-icomoon): [GPL](http://www.gnu.org/licenses/gpl.html) / [CC BY4.0](http://creativecommons.org/licenses/by/4.0/)

[1]: https://abhshkdz.mit-license.org/
[2]: https://chen1yi1.github.io/cast-deadlines.github.io/
[3]: http://www.conferenceranks.com/#