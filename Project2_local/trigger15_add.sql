-- description: All new bids must be placed at the time which matches the current time of your AuctionBase system.
PRAGMA foreign_keys = ON;
drop trigger if exists trigger15_add;
create trigger trigger15_add
before insert on Bids
for each row
when exists (
        Select * 
        from CurrentTime
        where new.Time <> CurrentTime.CurrTime
    )
begin
  select raise(rollback, 'All new bids must be placed at the time which matches the current time of your AuctionBase system.');
end;