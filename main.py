import utime

if __name__ == '__main__':

    print("Boot grace time...")
    utime.sleep(2)
    print("Running main...")

    from app import main
    # from scales import main
    # from wifi import main
    # from mqtt import main
    main()
