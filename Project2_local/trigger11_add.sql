-- description: No auction may have a bid before its start time or after its end time.
PRAGMA foreign_keys = ON;
drop trigger if exists trigger11_add;
create trigger trigger11_add
before insert on Bids
for each row
when exists (
        Select * 
        from Items
        where (Items.started > new.time or Items.ends < new.time) and Items.ItemID = new.ItemID
    )
begin
  select raise(rollback, 'No auction may have a bid before its start time or after its end time.');
end;